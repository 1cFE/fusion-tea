"use strict";

/**
 * Taxonomy page orchestration.
 *
 * State machine:
 *   OVERVIEW    — Constellation visible, no concept focused
 *   FOCUSED     — Neighborhood graph visible, taxonomy card + neighbor list in detail panel
 *   COMPARING   — FOCUSED + neighbor selected, comparison table + bridge nodes visible
 *
 * Transitions:
 *   OVERVIEW → FOCUSED:     Double-click constellation, OR single-click tree leaf
 *   FOCUSED → COMPARING:    Single-click neighbor (graph or list)
 *   COMPARING → COMPARING:  Single-click different neighbor
 *   COMPARING → FOCUSED:    Click graph background (deselect)
 *   FOCUSED → FOCUSED:      Double-click neighbor/bridge (re-center)
 *   Any → OVERVIEW:         "← Overview" button or Escape key
 */
(function () {

  // ---------------------------------------------------------------------------
  // State
  // ---------------------------------------------------------------------------

  var _viewMode = "overview"; // "overview" | "neighborhood"
  var _focusedId = null;
  var _comparingId = null;
  var _registry = {};           // concept_id → concept object
  var _similarityCache = {};    // "conceptId:topN" → similarity report
  var _sidebarCollapsed = false;
  var _neighborCount = 5;       // user-configurable, default 5

  // DOM references (set in init)
  var constellationContainer;
  var neighborhoodContainer;
  var taxonomyCardContainer;
  var comparisonContainer;
  var graphTitle;
  var graphSubtitle;
  var backButton;
  var toggleBtn;

  // ---------------------------------------------------------------------------
  // Init
  // ---------------------------------------------------------------------------

  async function init() {
    var loadingEl = document.getElementById("loading-state");
    var contentEl = document.getElementById("taxonomy-content");
    var errorEl = document.getElementById("error-state");

    loadingEl.style.display = "";
    contentEl.style.display = "none";
    errorEl.style.display = "none";

    // Cache DOM references
    constellationContainer = document.getElementById("constellation-container");
    neighborhoodContainer = document.getElementById("neighborhood-container");
    taxonomyCardContainer = document.getElementById("taxonomy-card-container");
    comparisonContainer = document.getElementById("comparison-container");
    graphTitle = document.getElementById("graph-title");
    graphSubtitle = document.getElementById("graph-subtitle");
    backButton = document.getElementById("back-to-overview");
    toggleBtn = document.getElementById("sidebar-toggle");

    // Fetch all initial data in parallel
    var treeData, constellationData, registryData, manifestData;
    try {
      var responses = await Promise.all([
        fetch("/api/taxonomy/tree"),
        fetch("/api/taxonomy/constellation"),
        fetch("/api/taxonomy/registry"),
        fetch("/api/manifest")
      ]);
      for (var i = 0; i < responses.length; i++) {
        if (!responses[i].ok) {
          throw new Error("API returned " + responses[i].status);
        }
      }
      treeData = await responses[0].json();
      constellationData = await responses[1].json();
      registryData = await responses[2].json();
      manifestData = await responses[3].json();
    } catch (err) {
      console.error("[taxonomy] Failed to load data:", err);
      loadingEl.style.display = "none";
      errorEl.style.display = "";
      return;
    }

    // Build registry lookup
    var concepts = registryData.concepts || [];
    var nameMap = {};
    for (var c = 0; c < concepts.length; c++) {
      _registry[concepts[c].concept_id] = concepts[c];
      nameMap[concepts[c].concept_id] = concepts[c].name;
    }

    // Share registry with TaxonomyCards for bridge family badge lookups
    TaxonomyCards.setRegistry(_registry);

    // Build set of analysis IDs that have cost model data available.
    // Manifest entries are keyed by analysis ID (e.g. "04", "05").
    var modeledIds = new Set();
    var manifestConcepts = (manifestData && manifestData.concepts) || [];
    for (var m = 0; m < manifestConcepts.length; m++) {
      modeledIds.add(manifestConcepts[m].concept_id);
    }
    TaxonomyCards.setModeledIds(modeledIds);

    // Render tree (single-click focuses)
    var treeContainer = document.getElementById("tree-container");
    TreeView.renderTreeView(treeContainer, treeData, handleFocus);
    TreeView.updateLeafLabels(nameMap);

    // Render constellation (single-click highlights, double-click focuses)
    Constellation.render(constellationContainer, constellationData,
      function onSingleClick(conceptId) {
        // Single-click in constellation: highlight the dot
        Constellation.highlight(conceptId);
      },
      function onDoubleClick(conceptId) {
        // Double-click in constellation: focus (switch to neighborhood)
        handleFocus(conceptId);
      }
    );

    // Set up sidebar toggle
    toggleBtn.addEventListener("click", function () {
      _sidebarCollapsed = !_sidebarCollapsed;
      var layout = document.querySelector(".taxonomy-layout");
      layout.classList.toggle("taxonomy-layout--collapsed", _sidebarCollapsed);
      toggleBtn.innerHTML = _sidebarCollapsed ? "&#8250;" : "&#8249;";
      toggleBtn.title = _sidebarCollapsed ? "Show decision tree" : "Hide decision tree";
      // Resize graph after CSS transition completes
      setTimeout(function () {
        if (_viewMode === "overview") {
          Plotly.Plots.resize(constellationContainer);
        } else if (_viewMode === "neighborhood") {
          NeighborhoodGraph.resize();
        }
      }, 350);
    });

    // Back to overview button
    backButton.addEventListener("click", function () {
      switchToOverview();
    });

    // Escape key → back to overview
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && _viewMode === "neighborhood") {
        switchToOverview();
      }
    });

    // Neighbor count control
    var neighborCountSelect = document.getElementById("neighbor-count-select");
    neighborCountSelect.addEventListener("change", function () {
      handleNeighborCountChange(parseInt(this.value, 10));
    });

    // Swap visibility
    loadingEl.style.display = "none";
    contentEl.style.display = "";
  }

  // ---------------------------------------------------------------------------
  // View mode switching
  // ---------------------------------------------------------------------------

  function switchToOverview() {
    if (_viewMode === "overview") return;

    // Fade out neighborhood
    neighborhoodContainer.style.opacity = "0";
    setTimeout(function () {
      neighborhoodContainer.style.display = "none";
      NeighborhoodGraph.destroy();

      constellationContainer.style.display = "";
      // Force a reflow before setting opacity for transition
      void constellationContainer.offsetHeight;
      constellationContainer.style.opacity = "1";
      Plotly.Plots.resize(constellationContainer);
    }, 300);

    graphTitle.textContent = "Design Space Overview";
    graphSubtitle.textContent = "Concepts positioned by design attribute similarity. Double-click to explore.";
    backButton.style.display = "none";
    document.getElementById("neighbor-count-control").style.display = "none";

    _viewMode = "overview";
    _focusedId = null;
    _comparingId = null;

    // Clear detail panel
    taxonomyCardContainer.innerHTML = "";
    comparisonContainer.innerHTML = "";

    // Clear constellation highlight
    Constellation.highlight(null);

    // Clear tree highlight
    TreeView.highlightTreeConcept(null);
  }

  function switchToNeighborhood(concept, report) {
    // Fade out constellation
    constellationContainer.style.opacity = "0";
    setTimeout(function () {
      constellationContainer.style.display = "none";

      neighborhoodContainer.style.display = "";
      // Force reflow
      void neighborhoodContainer.offsetHeight;
      neighborhoodContainer.style.opacity = "1";

      // Render the neighborhood graph (model-view: builds full graph once)
      NeighborhoodGraph.render(neighborhoodContainer, concept, report, _registry, {
        onCompare: handleCompare,
        onFocus: handleFocus,
        onDeselect: handleDeselect
      });
    }, 300);

    graphTitle.textContent = "Neighborhood of " + concept.name;
    graphSubtitle.textContent = "Click a neighbor to compare. Double-click to navigate.";
    backButton.style.display = "";
    document.getElementById("neighbor-count-control").style.display = "";
    _viewMode = "neighborhood";
  }

  // ---------------------------------------------------------------------------
  // Similarity data fetching (with cache)
  // ---------------------------------------------------------------------------

  function fetchSimilarity(conceptId) {
    var cacheKey = conceptId + ":" + _neighborCount;
    if (_similarityCache[cacheKey]) {
      return Promise.resolve(_similarityCache[cacheKey]);
    }
    var url = "/api/taxonomy/similarity/" + encodeURIComponent(conceptId)
      + "?top_n=" + _neighborCount;
    return fetch(url)
      .then(function (resp) {
        if (!resp.ok) throw new Error("Similarity API returned " + resp.status);
        return resp.json();
      })
      .then(function (report) {
        _similarityCache[cacheKey] = report;
        return report;
      });
  }

  // ---------------------------------------------------------------------------
  // Core handlers
  // ---------------------------------------------------------------------------

  /**
   * Focus on a concept — make it the center of the neighborhood graph.
   * Called from: tree single-click, constellation double-click, graph double-click.
   */
  function handleFocus(conceptId) {
    var concept = _registry[conceptId];
    if (!concept) {
      console.warn("[taxonomy] Unknown concept:", conceptId);
      return;
    }

    // Allow re-focus on same concept (e.g., from tree re-click after comparing)
    _focusedId = conceptId;
    _comparingId = null;

    // Show loading in comparison container
    comparisonContainer.innerHTML =
      '<div style="color: var(--color-text-muted); font-size: var(--font-size-sm); padding: var(--space-3);">Loading similarity...</div>';

    fetchSimilarity(conceptId).then(function (report) {
      // Only proceed if still focused on this concept
      if (_focusedId !== conceptId) return;

      // Switch view
      switchToNeighborhood(concept, report);

      // Update detail panel: taxonomy card + neighbor list
      TaxonomyCards.renderTaxonomyCard(taxonomyCardContainer, concept);
      TaxonomyCards.renderNeighborList(comparisonContainer, report.nearest, handleCompare);

      // Sync tree highlight
      TreeView.highlightTreeConcept(conceptId);
    }).catch(function (err) {
      console.warn("[taxonomy] Similarity fetch failed:", err);
      comparisonContainer.innerHTML = "";
    });
  }

  /**
   * Compare with a neighbor — show field-by-field comparison and bridge nodes.
   * Called from: graph single-click on neighbor, neighbor list click.
   */
  function handleCompare(neighborId) {
    if (neighborId === _comparingId) return;
    _comparingId = neighborId;

    var report = _similarityCache[_focusedId + ":" + _neighborCount];
    if (!report) return;

    var result = null;
    for (var i = 0; i < report.nearest.length; i++) {
      if (report.nearest[i].concept_id === neighborId) {
        result = report.nearest[i];
        break;
      }
    }
    if (!result) return;

    var focused = _registry[_focusedId];
    var neighbor = _registry[neighborId];

    // Show bridge nodes for this neighbor (visibility toggle)
    NeighborhoodGraph.compare(neighborId);

    // Get bridge data from the graph model for the comparison panel
    var bridges = NeighborhoodGraph.getBridgesForNeighbor(neighborId);

    // Update detail panel: comparison table
    TaxonomyCards.renderComparison(
      comparisonContainer, focused, neighbor, result,
      bridges, report.nearest, handleBridgeHighlight, handleCompare
    );
  }

  /**
   * Highlight a bridge node in the graph (pulse animation).
   * Called from: comparison panel bridge-ref clicks.
   */
  function handleBridgeHighlight(conceptId) {
    NeighborhoodGraph.highlightBridge(conceptId);
  }

  /**
   * Deselect the current neighbor comparison.
   * Called from: graph background click.
   */
  function handleDeselect() {
    if (!_comparingId) return;
    _comparingId = null;

    NeighborhoodGraph.clearComparison();

    // Restore neighbor list
    var report = _similarityCache[_focusedId + ":" + _neighborCount];
    if (report) {
      TaxonomyCards.renderNeighborList(comparisonContainer, report.nearest, handleCompare);
    }
  }

  /**
   * Change the number of neighbors displayed.
   * Called from: neighbor count dropdown.
   */
  function handleNeighborCountChange(newCount) {
    _neighborCount = newCount;
    if (_focusedId) {
      handleFocus(_focusedId);
    }
  }

  // ---------------------------------------------------------------------------
  // Bootstrap
  // ---------------------------------------------------------------------------

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
