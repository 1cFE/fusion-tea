"use strict";

/**
 * Taxonomy page orchestration.
 *
 * Fetches tree, constellation, and registry data on load.
 * Wires onConceptClick between tree, constellation, and cards.
 * Lazily fetches similarity reports on concept selection.
 */
(function () {
  var _registry = {};  // concept_id -> concept object
  var _selectedId = null;
  var _similarityCache = {};  // concept_id -> similarity report

  async function init() {
    var loadingEl = document.getElementById("loading-state");
    var contentEl = document.getElementById("taxonomy-content");
    var errorEl = document.getElementById("error-state");

    loadingEl.style.display = "";
    contentEl.style.display = "none";
    errorEl.style.display = "none";

    var treeData, constellationData, registryData;
    try {
      var responses = await Promise.all([
        fetch("/api/taxonomy/tree"),
        fetch("/api/taxonomy/constellation"),
        fetch("/api/taxonomy/registry")
      ]);
      for (var i = 0; i < responses.length; i++) {
        if (!responses[i].ok) {
          throw new Error("API returned " + responses[i].status);
        }
      }
      treeData = await responses[0].json();
      constellationData = await responses[1].json();
      registryData = await responses[2].json();
    } catch (err) {
      console.error("[taxonomy] Failed to load data:", err);
      loadingEl.style.display = "none";
      errorEl.style.display = "";
      return;
    }

    // Build registry lookup
    var concepts = registryData.concepts || [];
    var nameMap = {};  // id -> display name (for tree labels)
    for (var c = 0; c < concepts.length; c++) {
      _registry[concepts[c].concept_id] = concepts[c];
      nameMap[concepts[c].concept_id] = concepts[c].name;
    }

    // Render tree
    var treeContainer = document.getElementById("tree-container");
    TreeView.renderTreeView(treeContainer, treeData, onConceptClick);
    TreeView.updateLeafLabels(nameMap);

    // Render constellation
    var constContainer = document.getElementById("constellation-container");
    Constellation.render(constContainer, constellationData, onConceptClick);

    // Swap visibility
    loadingEl.style.display = "none";
    contentEl.style.display = "";
  }

  /**
   * Central concept selection handler — called by tree, constellation, and cards.
   */
  async function onConceptClick(conceptId) {
    if (conceptId === _selectedId) return;
    _selectedId = conceptId;

    var concept = _registry[conceptId];
    if (!concept) {
      console.warn("[taxonomy] Unknown concept:", conceptId);
      return;
    }

    // Update tree highlight
    TreeView.highlightTreeConcept(conceptId);

    // Update constellation highlight
    Constellation.highlight(conceptId);

    // Render taxonomy card
    var taxContainer = document.getElementById("taxonomy-card-container");
    TaxonomyCards.renderTaxonomyCard(taxContainer, concept);

    // Fetch and render similarity card (lazy, cached)
    var simContainer = document.getElementById("similarity-card-container");
    if (_similarityCache[conceptId]) {
      TaxonomyCards.renderSimilarityCard(simContainer, _similarityCache[conceptId], onConceptClick);
    } else {
      simContainer.innerHTML = '<div style="color: var(--color-text-muted); font-size: var(--font-size-sm); padding: var(--space-3);">Loading similarity...</div>';
      try {
        var resp = await fetch("/api/taxonomy/similarity/" + encodeURIComponent(conceptId));
        if (resp.ok) {
          var report = await resp.json();
          _similarityCache[conceptId] = report;
          // Only render if still the selected concept
          if (_selectedId === conceptId) {
            TaxonomyCards.renderSimilarityCard(simContainer, report, onConceptClick);
          }
        } else {
          console.warn("[taxonomy] Similarity fetch returned", resp.status);
          simContainer.innerHTML = "";
        }
      } catch (err) {
        console.warn("[taxonomy] Similarity fetch failed:", err);
        simContainer.innerHTML = "";
      }
    }
  }

  // Initialize when DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
